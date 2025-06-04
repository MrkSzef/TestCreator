import TestView from "@/components/other/TestView/TestView";
import TestNotFound from "@/components/other/TestNotFound/TestNotFound";
import axios from "axios";
import { useEffect, useState } from "react";
import { useParams } from "react-router";

export default function TestPage() {
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
        <>{stronaIstnieje ? <TestView></TestView> : <TestNotFound></TestNotFound>}</>
    );
}
