import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
} from "../../components/ui/dialog";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { useNavigate } from "react-router";

export default function ExamScore(Params: {
    OpenDialog: boolean;
    TestData: {
        pytania: { ID: string; tresc: string; odp: string[] }[];
        uzyskanePunkty: { punkty: number; pytania_bledne: number[] };
        odpowiedzi: { [ID: string]: string };
    };
}) {
    const navigate = useNavigate();
    const PytaniaID = Object.keys(Params.TestData.odpowiedzi);
    const Tresc = Params.TestData.pytania.reduce((acc, item) => {
        acc[item.ID] = item.tresc;
        return acc;
    }, {} as { [key: string]: string });

    return (
        <Dialog open={Params.OpenDialog}  onOpenChange={() => {navigate("/")}}>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>Wyniki Testu</DialogTitle>
                    <DialogDescription>Zdobyto {Params.TestData.uzyskanePunkty.punkty}/{Params.TestData.pytania.length} pkt</DialogDescription>
                    <DialogDescription>
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Wynik</TableHead>
                                    <TableHead>Pytanie</TableHead>
                                    <TableHead>Odpowiedz</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {PytaniaID.map((ID, index) => (
                                    <TableRow key={index}>
                                        {Params.TestData.uzyskanePunkty.pytania_bledne.includes(
                                            Number(ID)
                                        ) ? (
                                            <TableCell className="text-red-600">Błędne</TableCell>
                                        ) : (
                                            <TableCell className="text-green-600">Poprawne</TableCell>
                                        )}
                                        <TableCell>{Tresc[ID]}</TableCell>
                                        <TableCell>
                                            {
                                                Params.TestData.odpowiedzi[
                                                    Number(ID)
                                                ]
                                            }
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </DialogDescription>
                </DialogHeader>
            </DialogContent>
        </Dialog>
    );
}