import TestView from "@/components/other/TestView/TestView";
import WavyText from "@/components/other/WavyText/WavyTest";
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
        <>{stronaIstnieje ? <TestView></TestView> : <WavyText></WavyText>}</>
    );
}
