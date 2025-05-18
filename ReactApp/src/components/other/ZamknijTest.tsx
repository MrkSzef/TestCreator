import React from "react";
import { Button } from "../ui/button";
import { useState, useEffect } from "react";
import axios from "axios";

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
        <div>
            <Button
                disabled={Params.testId === undefined}
                onClick={() => ZamknijTestApiCall(Params.testId)}
            >
                Zamknij test
            </Button>
        </div>
    );
}
