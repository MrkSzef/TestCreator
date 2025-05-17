function generateSteps(text: string): string[] {
  const steps: string[] = [];
  for (let i = 1; i <= text.length; i++) {
    steps.push(text.substring(0, i));
  }
  return steps;
}

export default generateSteps;