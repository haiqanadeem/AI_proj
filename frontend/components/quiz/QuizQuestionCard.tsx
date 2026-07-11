import { QuizQuestion } from "@/types/api";

export function QuizQuestionCard({ 
  question, 
  index,
  selectedValue, 
  onSelect 
}: { 
  question: QuizQuestion; 
  index: number;
  selectedValue: string; 
  onSelect: (val: string) => void;
}) {
  return (
    <div className="p-6 bg-card border border-border rounded-lg shadow-sm mb-6">
      <h3 className="text-xl font-bold mb-4">Question {index + 1}: {question.question}</h3>
      <div className="space-y-3">
        {question.options.map((opt, i) => {
          const letter = String.fromCharCode(65 + i);
          const isSelected = selectedValue === letter;
          return (
            <label 
              key={letter} 
              className={`flex items-center p-4 border rounded cursor-pointer focus-within:ring-2 focus-within:ring-primary ${isSelected ? "border-primary bg-primary/10" : "border-border hover:bg-muted"}`}
            >
              <input
                type="radio"
                name={`question-${question.id}`}
                value={letter}
                checked={isSelected}
                onChange={() => onSelect(letter)}
                className="w-4 h-4 text-primary bg-background border-border focus:ring-primary mr-3 sr-only focus:not-sr-only"
              />
              <span className="font-bold mr-2">{letter}:</span>
              <span>{opt}</span>
            </label>
          );
        })}
      </div>
    </div>
  );
}
