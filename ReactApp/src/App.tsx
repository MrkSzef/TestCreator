import "./App.css";
import Welcome from "./components/other/WelcomeAnimation/WelcomeAnimation";
import {
    Card,
    CardHeader,
    CardTitle,
} from "./components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import JoinForm from "./components/other/JoinForm/JoinForm";
import CreateForm from "./components/other/CreateForm/CreateForm";


function App() {
    return (
        <>
            <div className="flex flex-col gap-10 h-60 justify-between">
                <Welcome></Welcome>
                <div className="flex flex-row justify-center">
                    <Tabs
                        defaultValue="account"
                        className="w-[400px] flex gap-5"
                    >
                        <TabsList className="grid w-full grid-cols-2 gap-3">
                            <TabsTrigger value="join">
                                Dołącz do testu
                            </TabsTrigger>
                            <TabsTrigger value="create">
                                Utwórz Test
                            </TabsTrigger>
                        </TabsList>
                        <TabsContent value="join">
                            <Card>
                                <CardHeader>
                                    <CardTitle>Dołącz do testu</CardTitle>
                                </CardHeader>

                                <JoinForm></JoinForm>
                            </Card>
                        </TabsContent>
                        <TabsContent value="create">
                            <Card>
                                <CardHeader>
                                    <CardTitle>Utwórz Test</CardTitle>
                                </CardHeader>

                                <CreateForm></CreateForm>

                            </Card>
                        </TabsContent>
                    </Tabs>
                </div>
            </div>
        </>
    );
}

export default App;
