import { 
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import { useDeletePrompt } from '../api/prompts_queries';
import { usePromptsStore } from '../stores/prompts_store';

interface DeletePromptDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  promptId: string | null;
}

export function DeletePromptDialog({ open, onOpenChange, promptId }: DeletePromptDialogProps) {
  const deleteMutation = useDeletePrompt();
  const { resetEditor, setSelectedPrompt } = usePromptsStore();

  const handleDelete = async () => {
    if (!promptId) return;
    
    await deleteMutation.mutateAsync(promptId);
    resetEditor();
    setSelectedPrompt(null);
    onOpenChange(false);
  };

  return (
    <AlertDialog open={open} onOpenChange={onOpenChange}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
          <AlertDialogDescription>
            This action cannot be undone. This will permanently delete the prompt template and remove it from our servers.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction 
            onClick={handleDelete} 
            className="bg-destructive hover:bg-destructive/90"
          >
            Delete
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
