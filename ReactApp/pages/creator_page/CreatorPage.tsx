import { useParams } from "react-router";
import ZamknijTest from "@/components/other/ZamknijTest";
import TeacherView from "@/components/other/TeacherView/TeacherView";


export default function CreatorPage() {
  const { id } = useParams();

  return (
    <div className="flex flex-col gap-3">
      <ZamknijTest testId={id}></ZamknijTest>
      <TeacherView testId={id!}></TeacherView>
    </div>
  );
}
