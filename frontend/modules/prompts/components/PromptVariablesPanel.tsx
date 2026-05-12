import { usePromptVariables } from '../hooks/usePromptVariables';
import { usePromptsStore } from '../stores/prompts_store';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';

export function PromptVariablesPanel() {
  const variables = usePromptVariables();
  const { previewVariables, updatePreviewVariable } = usePromptsStore();

  if (variables.length === 0) {
    return (
      <div className="p-4 text-center text-gray-500 text-sm bg-gray-900 rounded border border-gray-800">
        No variables detected in prompt. Use {'{{variable}}'} syntax to add dynamic values.
      </div>
    );
  }

  return (
    <div className="space-y-4 p-4 bg-gray-900 rounded border border-gray-800">
      <h3 className="text-sm font-semibold text-white uppercase tracking-wider">Detected Variables</h3>
      <div className="grid grid-cols-1 gap-4">
        {variables.map((variable: any) => (
          <div key={variable.key} className="space-y-1">
            <div className="flex justify-between items-center">
              <Label htmlFor={`var-${variable.key}`} className="text-xs text-gray-300 font-mono">
                {variable.key}
              </Label>
              {variable.required && <Badge variant="destructive" className="scale-75">Required</Badge>}
            </div>
            <Input
              id={`var-${variable.key}`}
              value={previewVariables[variable.key] || variable.default_value || ''}
              onChange={(e) => updatePreviewVariable(variable.key, e.target.value)}
              placeholder={`Enter value for ${variable.key}`}
              className="bg-gray-950 border-gray-700 text-sm h-8"
            />
            <p className="text-[10px] text-gray-500">{variable.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
