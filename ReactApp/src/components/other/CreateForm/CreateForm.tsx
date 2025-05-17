import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

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

const formSchema = z.object({
    file: z
        .instanceof(File)
        .nullable()
        .refine((file) => file !== null && file.name.endsWith(".csv"), {
            message: "Podaj odpowiedni plik .csv",
        }),
});

export default function ProfileForm() {
    const form = useForm<{ file: File | null }>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            file: null,
        },
    });

    function onSubmit(values: z.infer<typeof formSchema>) {
        console.log(values);
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
                </CardContent>
                <CardFooter>
                    <Button type="submit">Utwórz</Button>
                </CardFooter>
            </form>
        </Form>
    );
}
