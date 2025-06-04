import { useParams } from "react-router";
import ZamknijTest from "@/components/other/CloseTest";
import TeacherView from "@/components/other/TeacherView/TeacherView";
import DeleteTest from "@/components/other/DeleteTest";
import { useEffect, useState } from "react";
import axios from "axios";
import "@/styles/globals.css";
import TestNotFound from "@/components/other/TestNotFound/TestNotFound";

export default function CreatorPage() {
    const { id } = useParams();
    const [stronaIstnieje, setStronaIstnieje] = useState(false);

    useEffect(() => {
        axios
            .get(`http://localhost:8000/uczen/test/${id}/zamkniety`)
            .then(() => {
                setStronaIstnieje(true);
            })
            .catch(() => {
                setStronaIstnieje(false);
            });
    }, [stronaIstnieje]);

    return (
        <div className="flex flex-col gap-3">
            {stronaIstnieje ? (
                <>
                    <ZamknijTest testId={id!}></ZamknijTest>
                    <TeacherView testId={id!}></TeacherView>
                    <DeleteTest testId={id!}></DeleteTest>
                </>
            ) : (
                <TestNotFound></TestNotFound>
            )}
        </div>
    );
}
