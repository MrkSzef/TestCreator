import { useState, useEffect } from "react";
import './TypingAnimation.css';
import generateSteps from "./GenerateString";

const Text = "Utwórz Swój Własny Test";
const steps = generateSteps(Text);

function Welcome() {

  const [currentText, setCurrentText] = useState('');
  const [currentStep, setCurrentStep] = useState(0);
  const timeout = 120;
  
  useEffect(() => {
    if (currentStep < steps.length) {
      const timer = setTimeout(() => {
        setCurrentText(steps[currentStep]);
        setCurrentStep(currentStep + 1);
      }, timeout + (Math.random() * 80) * (Math.random()>0.75 ? 1:-0.5));
      
      return () => clearTimeout(timer);
    }
  }, [currentStep]);

  return (
      <div className="flex flex-row gap-6">
        {currentText.split(' ').map((word, index) => <span className="typing-text" key={index} style={{
      fontFamily: 'monospace',
      fontSize: '2.5rem',
      letterSpacing: '2px',
      minHeight: '1.5em',
      position: 'relative'
    }}>{word.split('').map((char, index) => (
        <span 
          key={index} 
          className="letter text-zinc-300 text-shadow-zinc-200 text-shadow-3xs"
          style={{
              display: 'inline-block',
              opacity: 1,
              transform: 'translateY(0)',
              transition: 'opacity 0.1s ease-in-out, transform 0.1s ease-in-out',
              animation: 'fadeIn 0.1s ease-in-out'
            }}
        >
          {char}
        </span>
      ))} </span>)}
      <span 
        style={{
          opacity: currentText !== Text? 0:1,
          transition: 'opacity 0.2s',
          transform: 'translateX(-25px) translateY(-10px)',
          height: '1.5em',
          animation: `blink 1s infinite ${Text.split('').length * timeout+250}ms`
        }}
        className="letter"
      >|</span>
      </div>
  );
}

export default Welcome;


