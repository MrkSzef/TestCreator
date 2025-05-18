import { useParams } from "react-router";
import ZamknijTest from "@/components/other/ZamknijTest";

export default function CreatorPage() {
  const { id } = useParams();

  return (
    <div className="flex flex-row gap-3">
      <p>Test Join id: {id}</p>
      <ZamknijTest testId={id}></ZamknijTest>
      
    </div>
  );
}
