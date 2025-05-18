import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import axios from "axios";
import { useParams } from "react-router";
import { useEffect, useState } from "react";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import "../../src/styles/globals.css";
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

function GetTest(odpowiedzi: { [key: string]: string }) {
    console.log(odpowiedzi);
}

type Pytanie = {
    ID: string | number;
    tresc: string;
    odp: string[];
};
const formSchema = z.object({
    name: z.string(),
    surname: z.string(),
});

export default function TestPage() {
    let odpowiedzi: { [key: string]: string } = {};
    const { id } = useParams();
    const [pytania, setPytania] = useState<Pytanie[]>([]);

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            name: "",
            surname: "",
        },
    });

    // 2. Define a submit handler.
    function onSubmit(values: z.infer<typeof formSchema>) {
        // Do something with the form values.
        // ✅ This will be type-safe and validated.
        console.log(values);
    }

    // API REQUEST
    useEffect(() => {
        axios
            .get(`http://localhost:8000/uczen/arkusz/${id}`)
            .then((res) => {
                console.log(res.data);
                setPytania(res.data.pytania);
            })
            .catch((err) => {
                console.log(err.response.data);
            });
    }, []);

    return (
        <Card>
            <CardHeader>
                <CardTitle>Test {id}</CardTitle>
                <Button onClick={() => GetTest(odpowiedzi)}>ziemniak</Button>
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
                            <RadioGroup onValueChange={(odpowiedz) => {odpowiedzi[pytanie.ID] = odpowiedz}} className="pb-5 pt-5">
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
    );
}
