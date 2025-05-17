import React from "react";
import { useParams } from "react-router";

export default function CreatorPage() {
  const { id } = useParams();

  return (
    <div>
      <h1>Creator Page {id}</h1>
    </div>
  );
}
