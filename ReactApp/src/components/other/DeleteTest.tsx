import axios from "axios";
import {
    Card,
    CardContent,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";
import { useState } from "react";
import { useNavigate } from "react-router";

function DeleteTestApiCall(id: string | undefined) {
    axios.delete(`http://localhost:8000/nauczyciel/test/${id}`).catch((err) => {
        console.log(err.response.data);
    });
}

export default function DeleteTest(Params: { testId: string }) {
    const navigate = useNavigate();
    const [openDeleteDialog, setOpenDeleteDialog] = useState(false);


    function HandleDestructClick(testId: string) {
        DeleteTestApiCall(testId);
        navigate("/");
    }


    return (
        <>
            <Dialog open={openDeleteDialog} onOpenChange={setOpenDeleteDialog}>
                <DialogContent className="space-y-6">
                    <DialogHeader>
                        <DialogTitle>
                            Czy na pewno chcesz usunąć ten test?
                        </DialogTitle>
                        <DialogDescription>
                            Czynność jest nieodwracalna
                        </DialogDescription>
                    </DialogHeader>
                    <Button
                        variant={"destructive"}
                        onClick={() => HandleDestructClick(Params.testId)}
                    >
                        Usun
                    </Button>
                </DialogContent>
            </Dialog>
            <Card>
                <CardContent className="flex flex-row justify-around gap-4">
                    <Button
                        variant="destructive"
                        disabled={Params.testId === undefined}
                        onClick={() => setOpenDeleteDialog(true)}
                    >
                        Usuń test
                    </Button>
                </CardContent>
            </Card>
        </>
    );
}
