import { AlertCircle, CheckCircle } from 'lucide-react';
import { usePromptValidation } from '../hooks/usePromptValidation';
import { cn } from '@/utils/cn';

export function PromptValidationPanel() {
  const errors = usePromptValidation();
  const isValid = errors.length === 0;

  return (
    <div className={cn(
      "p-3 rounded-md border text-sm",
      isValid 
        ? "bg-green-950/30 border-green-900/50 text-green-400" 
        : "bg-red-950/30 border-red-900/50 text-red-400"
    )}>
      <div className="flex items-center gap-2 mb-2 font-semibold">
        {isValid ? <CheckCircle className="h-4 w-4" /> : <AlertCircle className="h-4 w-4" />}
        {isValid ? 'Valid Prompt' : `Validation Errors (${errors.length})`}
      </div>
      
      {!isValid && (
        <ul className="list-disc list-inside space-y-1 text-xs opacity-90">
          {errors.map((err, idx) => (
            <li key={idx}>
              <span className="font-mono uppercase mr-2">[{err.type}]</span>
              {err.message}
              {err.variable && <span className="text-yellow-400 ml-1">(Var: {err.variable})</span>}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
