import React from "react";
import { Button } from "../ui/button";
import { useState, useEffect } from "react";
import axios from "axios";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";

function ZamknijTestApiCall(id: string | undefined) {
    axios
        .get(`http://localhost:8000/nauczyciel/test/${id}/zamknij`)
        .then((res) => {
            console.log(res.data);
        })
        .catch((err) => {
            console.log(err.response.data);
        });
}

export default function ZamknijTest(Params: { testId: string | undefined }) {
    return (
        <Card>
            <CardHeader>
                <CardTitle>Test {Params.testId}</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-row justify-around">
                <Button
                    disabled={Params.testId === undefined}
                    onClick={() => ZamknijTestApiCall(Params.testId)}
                >
                    Zamknij test
                </Button>

                <Button
                    variant="secondary"
                    onClick={() =>
                        navigator.clipboard.writeText(Params.testId!)
                    }
                >
                    Kopiuj Kod Testu
                </Button>
            </CardContent>
        </Card>
    );
}
