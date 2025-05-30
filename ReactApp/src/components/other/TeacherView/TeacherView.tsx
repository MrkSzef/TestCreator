import { useState, useEffect } from "react";
import useWebSocket from "react-use-websocket";
import type { ParticipantAnswer } from "@/interfaces/InfoWebsocketInterface";

import axios from "axios";
import {
    Card,
    CardContent,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";

export default function TeacherView(params: { testId: string }) {
    const { lastMessage } = useWebSocket(
        `ws://localhost:8000/nauczyciel/test/${params.testId}/info/ws`
    );
    const [data, setdata] = useState<ParticipantAnswer[]>([]);
    useEffect(() => {
        if (lastMessage) {
            setdata(JSON.parse(lastMessage.data).uczestnicy_odpowiedzi);
        }
    }, [lastMessage]);
    useEffect(() => {
        axios
            .get(`http://localhost:8000/nauczyciel/test/${params.testId}/info`)
            .then((res) => {
                setdata(res.data.uczestnicy_odpowiedzi);
            })
            .catch((err) => {
                console.log(err);
            });
    }, [params.testId]);

    return (
        <Card>
            {data.length === 0 ? (
                <CardHeader>
                    <CardTitle>Brak Wyników</CardTitle>
                </CardHeader>
            ) : (
                <CardHeader>
                    <CardTitle>Wyniki Uczniów</CardTitle>
                </CardHeader>
            )}
            <CardContent
                className={`grid grid-cols-${
                    data.length <= 3 ? data.length : 3
                } space-x-4 space-y-4`}
            >
                {data.map((wyniki_ucznia: ParticipantAnswer) => (
                    <Card>
                        <CardHeader>
                            <CardTitle>
                                {wyniki_ucznia.uczen.imie}{" "}
                                {wyniki_ucznia.uczen.nazwisko}
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <Table>
                                <TableCaption></TableCaption>
                                <TableHeader>
                                    <TableRow>
                                        <TableHead className="text-center">
                                            Nr Pytania
                                        </TableHead>
                                        <TableHead className="text-center">
                                            Wynik
                                        </TableHead>
                                        <TableHead className="text-center">
                                            Odpowiedz
                                        </TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {Object.keys(wyniki_ucznia.klucz_odp).map(
                                        (IDPytania: string) => (
                                            <TableRow>
                                                <TableCell>
                                                    {IDPytania}
                                                </TableCell>
                                                {wyniki_ucznia.wynik.pytania_bledne.includes(
                                                    Number(IDPytania)
                                                ) ? (
                                                    <TableCell className="text-red-600">
                                                        Błędne
                                                    </TableCell>
                                                ) : (
                                                    <TableCell className="text-green-600">
                                                        Poprawne
                                                    </TableCell>
                                                )}
                                                <TableCell>
                                                    {
                                                        wyniki_ucznia.klucz_odp[
                                                            IDPytania
                                                        ]
                                                    }
                                                </TableCell>
                                            </TableRow>
                                        )
                                    )}
                                </TableBody>
                            </Table>
                        </CardContent>
                        <CardFooter className="justify-center flex-col">
                            <p className="text-center">
                                Wynik: {wyniki_ucznia.wynik.punkty}/
                                {Object.keys(wyniki_ucznia.klucz_odp).length}{" "}
                                pkt{" "}
                            </p>
                            <p>{`[ ${(
                                (wyniki_ucznia.wynik.punkty /
                                    Object.keys(wyniki_ucznia.klucz_odp)
                                        .length) *
                                100
                            ).toFixed(1)}% ]`}</p>
                        </CardFooter>
                    </Card>
                ))}
            </CardContent>
        </Card>
    );
}
