import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { useNavigate } from "react-router";

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
    code: z.string().length(32, {
        message: "Kod Testu ma 32 litery",
    })
});

export default function JoinForm() {
    let navigate = useNavigate();

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            code: ""
        },
    });

    function onSubmit(values: z.infer<typeof formSchema>) {
        navigate(`/test/${values.code}`);
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                <CardContent className="space-y-4 gap-3">

                    <FormField
                        control={form.control}
                        name="code"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Kod Testu</FormLabel>
                                <FormControl>
                                    <Input
                                        id="code"
                                        placeholder="H1LSNMSD9COWEK"
                                        {...field}
                                    />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                </CardContent>
                <CardFooter>
                    <Button type="submit">Dołącz</Button>
                </CardFooter>
            </form>
        </Form>
    );
}
