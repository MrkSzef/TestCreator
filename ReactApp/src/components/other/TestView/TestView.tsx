import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import axios from "axios";
import { useParams } from "react-router";
import { useEffect, useState } from "react";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import ExamScore from "@/components/other/ExamScore";

type Pytanie = {
    ID: string;
    tresc: string;
    odp: string[];
};

const formSchema = z.object({
    name: z.string().regex(/^[A-ZĘÓĄŚŁŻŹĆŃ][a-zęóąśłżźćń]*$/, {
        message: "Podaj poprawne imie",
    }),
    surname: z.string().regex(/^[A-ZĘÓĄŚŁŻŹĆŃ][a-zęóąśłżźćń]*$/, {
        message: "Podaj poprawne nazwisko",
    }),
});

export default function TestPage() {
    const { id } = useParams();
    const [odpowiedzi, setOdpowiedzi] = useState<{ [key: string]: string }>({});
    const [uzyskanePunkty, setUzyskanePunkty] = useState<{
        punkty: number;
        pytania_bledne: number[];
    }>({ punkty: 0, pytania_bledne: [] });
    const [pytania, setPytania] = useState<Pytanie[]>([]);
    const [oddane, setOddane] = useState(false);

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            name: "",
            surname: "",
        },
    });

    function onSubmit(values: z.infer<typeof formSchema>) {
        const data = {
            imie: values.name,
            nazwisko: values.surname,
            odp: odpowiedzi,
        };
        if (!oddane) {
            axios
                .post(`http://localhost:8000/uczen/arkusz/${id}/odaji`, data)
                .then((res) => {
                    console.log(res.status);
                    console.log(res.data);

                    if (res.status == 200) {
                        setOddane(true);
                        setUzyskanePunkty(res.data);
                    }
                })
                .catch((err) => {
                    if (err.status == 400) {
                        toast("Nie zaznaczono wszystkich odpowiedzi", {
                            description: `Oddano ${
                                err.response.data.detail[1].split(": ")[1]
                            }/${
                                err.response.data.detail[2].split(": ")[1]
                            } Odpowiedzi`,
                            action: {
                                label: "Usuń",
                                onClick: () => console.log("Undo"),
                            },
                        });
                    }
                    console.log(err.response.data);
                });
        }
    }


    useEffect(() => {
        axios
            .get(`http://localhost:8000/uczen/arkusz/${id}`)
            .then((res) => {
                console.log(res.data);

                setPytania(
                    res.data.pytania.map((pytanie: any) => ({
                        ...pytanie,
                        ID: String(pytanie.ID),
                    }))
                );
            })
            .catch((err) => {
                console.log(err.response.data);
            });
    }, []);

    return (
        <>
            <ExamScore
                OpenDialog={oddane}
                TestData={{ pytania, uzyskanePunkty, odpowiedzi }}
            ></ExamScore>
            <Card>
                <CardHeader>
                    <CardTitle>Test {id}</CardTitle>
                </CardHeader>
                <CardContent className="flex flex-col gap-5">
                    <Form {...form}>
                        <form onSubmit={form.handleSubmit(onSubmit)}>
                            <div className="flex flex-row gap-2">
                                <FormField
                                    control={form.control}
                                    name="name"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Imie</FormLabel>
                                            <FormControl>
                                                <Input
                                                    placeholder="Jan"
                                                    {...field}
                                                />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                                <FormField
                                    control={form.control}
                                    name="surname"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Nazwisko</FormLabel>
                                            <FormControl>
                                                <Input
                                                    placeholder="Kowalski"
                                                    {...field}
                                                />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                                <div className="flex items-end">
                                    <Button type="submit">Oddaj Test</Button>
                                </div>
                            </div>
                        </form>
                    </Form>
                    <div className="flex flex-col divide-y-2 divide-dashed divide-gray-400">
                        {pytania.map((pytanie) => {
                            return (
                                <RadioGroup
                                    onValueChange={(odpowiedz) => {
                                        setOdpowiedzi({
                                            ...(odpowiedzi || {}),
                                            [pytanie.ID]: odpowiedz,
                                        });
                                    }}
                                    className="pb-5 pt-5 pytanie"
                                >
                                    <Label className="text-xl">
                                        {pytanie.tresc}
                                    </Label>
                                    {pytanie.odp.map((odpowiedz, idx) => (
                                        <div
                                            className="flex items-center space-x-2"
                                            key={idx}
                                        >
                                            <RadioGroupItem
                                                value={odpowiedz}
                                                id={`odp-${pytanie.ID}-${idx}`}
                                            />
                                            <Label
                                                className="text-md text-gray-200"
                                                htmlFor={`odp-${pytanie.ID}-${idx}`}
                                            >
                                                {odpowiedz}
                                            </Label>
                                        </div>
                                    ))}
                                </RadioGroup>
                            );
                        })}
                    </div>
                </CardContent>
            </Card>
        </>
    );
}
