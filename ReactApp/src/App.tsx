import { useState } from 'react'
import { Button } from './components/ui/button'
import './App.css'
import Welcome from './components/other/WelcomeAnimation/WelcomeAnimation'

//Animations to do

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <div className='flex flex-col gap-10 h-60 justify-between'>
      <Welcome></Welcome>
      <div className='flex flex-row justify-center'>
        <Button size={'lg'} className='scale-100 hover:scale-115 active:scale-105'>Utwórz Test</Button>
      </div>
    </div>
    </>
  )
}

export default App
