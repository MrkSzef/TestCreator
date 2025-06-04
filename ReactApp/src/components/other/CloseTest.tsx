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
import { useState } from "react";
import { useNavigate } from "react-router";

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
    const navigate = useNavigate();
    const [openDeleteDialog, setOpenDeleteDialog] = useState(false);

    function HandleCloseClick(testId: string) {
        ZamknijTestApiCall(testId);
        navigate("/");
    }
    return (
        <>
            <Dialog open={openDeleteDialog} onOpenChange={setOpenDeleteDialog}>
                <DialogContent className="space-y-6">
                    <DialogHeader>
                        <DialogTitle>
                            Czy na pewno chcesz zamknąć ten test?
                        </DialogTitle>
                        <DialogDescription>
                            Czynność jest nieodwracalna
                        </DialogDescription>
                    </DialogHeader>
                    <Button
                        variant={"destructive"}
                        onClick={() => HandleCloseClick(Params.testId!)}
                    >
                        Zamknij
                    </Button>
                </DialogContent>
            </Dialog>
            <Card>
                <CardHeader>
                    <CardTitle>Test</CardTitle>
                    <CardDescription>{Params.testId}</CardDescription>
                </CardHeader>
                <CardContent className="flex flex-row justify-around gap-4">
                    <Button
                        disabled={Params.testId === undefined}
                        onClick={() => setOpenDeleteDialog(true)}
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
        </>
    );
}


