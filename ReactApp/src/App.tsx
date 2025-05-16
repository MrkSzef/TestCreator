import { useState } from "react";
import { Button } from "./components/ui/button";
import "./App.css";
import Welcome from "./components/other/WelcomeAnimation/WelcomeAnimation";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "./components/ui/card";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import JoinForm from "./components/other/JoinForm/JoinForm";
//Animations to do

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
                                <CardContent className="space-y-1">
                                    <Label htmlFor="file">Plik .csv</Label>
                                    <Input id="file" type="file" />
                                </CardContent>
                                <CardFooter>
                                    <Button>Utwórz</Button>
                                </CardFooter>
                            </Card>
                        </TabsContent>
                    </Tabs>
                </div>
            </div>
        </>
    );
}

export default App;
