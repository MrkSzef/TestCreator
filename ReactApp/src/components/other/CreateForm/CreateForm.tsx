import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import axios from "axios";

import { Button } from "@/components/ui/button";
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { CardContent, CardFooter } from "@/components/ui/card";
import FormData from "form-data";
import { useNavigate } from "react-router";

const formSchema = z.object({
    file: z
        .instanceof(File)
        .nullable()
        .refine((file) => file !== null && file.name.endsWith(".csv"), {
            message: "Podaj odpowiedni plik .csv",
        }),
    liczba_pytan: z.string().refine((val) => !Number.isNaN(parseInt(val)), {
        message: "Expected number, received a string"
  }),
});

export default function CreateForm() {
    let navigate = useNavigate();

    const form = useForm<{ file: File | null; liczba_pytan: string }>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            file: null,
            liczba_pytan: "1",
        },
    });

    function onSubmit(values: z.infer<typeof formSchema>) {
        // Data to send
        const formData = new FormData();
        formData.append("liczba_pytan", values.liczba_pytan);
        formData.append("plik_csv", values.file, {
            filename: "pytania.csv",
            contentType: "text/csv",
        });

        // Post request
        axios
            .post("http://localhost:8000/nauczyciel/test/stworz", formData, {
                headers: {
                    accept: "application/json",
                },
            })
            .then((res) => {
                navigate(`/creator/${res.data.test_id}`);
            })
            .catch((err) => {
                console.log(err.response.data);
            });
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                <CardContent className="space-y-4 gap-3">
                    <FormField
                        control={form.control}
                        name="file"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Plik .csv</FormLabel>
                                <FormControl>
                                    <Input
                                        id="file"
                                        type="file"
                                        onChange={(e) => {
                                            const file =
                                                e.target.files &&
                                                e.target.files[0]
                                                    ? e.target.files[0]
                                                    : null;
                                            field.onChange(file);
                                        }}
                                        onBlur={field.onBlur}
                                        name={field.name}
                                        ref={field.ref}
                                    />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />

                    <FormField
                        control={form.control}
                        name="liczba_pytan"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Liczba Pytań</FormLabel>
                                <FormControl>
                                    <Input
                                        id="liczba_pytan"
                                        type="number"
                                        {...field}
                                    />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                </CardContent>
                <CardFooter>
                    <Button type="submit">Utwórz</Button>
                </CardFooter>
            </form>
        </Form>
    );
}
