import { useState } from 'react'
import { Button } from './components/ui/button'
import './App.css'
import Welcome from './components/other/WelcomeAnimation/WelcomeAnimation'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./components/ui/card"
import { Input } from "./components/ui/input"
import { Label } from "./components/ui/label"
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "./components/ui/tabs"

//Animations to do

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <div className='flex flex-col gap-10 h-60 justify-between'>
      <Welcome></Welcome>
      <div className='flex flex-row justify-center'>
      <Tabs defaultValue="account" className="w-[400px]">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="join">Dołącz do testu</TabsTrigger>
          <TabsTrigger value="create">Utwórz Swój Własny Test</TabsTrigger>
        </TabsList>
        <TabsContent value="join">
          <Card>
            <CardHeader>
              <CardTitle>Dołącz do testu</CardTitle>
              <CardDescription>
                Make changes to your account here. Click save when you're done.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-1">
                <Label htmlFor="name">Imię</Label>
                <Input id="name" defaultValue="Jan" />
              </div>
              <div className="space-y-1">
                <Label htmlFor="surname">Nazwisko</Label>
                <Input id="surname" defaultValue="Kowalski" required/>
              </div>
              <div className="space-y-1">
                <Label htmlFor="code">Kod Testu</Label>
                <Input id="code" defaultValue="H1LSNMSD9COWEK" />
              </div>
            </CardContent>
            <CardFooter>
              <Button>Dołącz</Button>
            </CardFooter>
          </Card>
        </TabsContent>
        <TabsContent value="create">
          <Card>
            <CardHeader>
              <CardTitle>Utwórz Swój Własny Test</CardTitle>
            </CardHeader>
            <CardContent className="space-y-1">
              <Button>Utwórz Test</Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
      </div>
    </div>
    </>
  )
}

export default App
