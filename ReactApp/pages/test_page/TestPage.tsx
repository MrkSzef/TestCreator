import { useParams } from "react-router";


export default function TestPage(){
    const { id } = useParams();

    return (
        <div>
        <h1>Test Page {id}</h1>
        </div>
    );
};
