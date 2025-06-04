import { Button } from "../ui/button";
import axios from "axios";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";


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
                <CardTitle>Test</CardTitle>
                <CardDescription>{Params.testId}</CardDescription>
            </CardHeader>
            <CardContent className="flex flex-row justify-around gap-4">
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
