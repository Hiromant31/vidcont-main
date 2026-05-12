'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { promptsApi } from '@/services/api/settings';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import type { PromptTemplate } from '@/types';

export default function PromptsPage() {
  const queryClient = useQueryClient();
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingPrompt, setEditingPrompt] = useState<PromptTemplate | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    stage: 'story',
    content: '',
    genre: 'general',
    style: 'narrative',
  });

  const { data: prompts = [], isLoading, error } = useQuery({
    queryKey: ['prompts'],
    queryFn: () => promptsApi.getAll(),
  });

  const createMutation = useMutation({
    mutationFn: (data: Partial<PromptTemplate>) => promptsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['prompts'] });
      setShowCreateForm(false);
      resetForm();
      alert('Prompt created successfully!');
    },
    onError: (error) => {
      alert(`Failed to create prompt: ${error.message}`);
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<PromptTemplate> }) => 
      promptsApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['prompts'] });
      setEditingPrompt(null);
      resetForm();
      alert('Prompt updated successfully!');
    },
    onError: (error) => {
      alert(`Failed to update prompt: ${error.message}`);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => promptsApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['prompts'] });
      alert('Prompt deleted successfully!');
    },
    onError: (error) => {
      alert(`Failed to delete prompt: ${error.message}`);
    },
  });

  const resetForm = () => {
    setFormData({
      name: '',
      stage: 'story',
      content: '',
      genre: 'general',
      style: 'narrative',
    });
  };

  const handleEdit = (prompt: PromptTemplate) => {
    setEditingPrompt(prompt);
    setFormData({
      name: prompt.name || '',
      stage: prompt.stage || prompt.type || 'story',
      content: prompt.content || '',
      genre: prompt.genre || 'general',
      style: prompt.style || 'narrative',
    });
    setShowCreateForm(false);
  };

  const handleSubmit = () => {
    if (editingPrompt) {
      updateMutation.mutate({ id: editingPrompt.template_id, data: formData });
    } else {
      createMutation.mutate(formData);
    }
  };

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading prompts: {error.message}</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Prompts</h1>
        <Button onClick={() => {
          setShowCreateForm(!showCreateForm);
          setEditingPrompt(null);
          resetForm();
        }}>
          {showCreateForm ? 'Cancel' : 'Create Prompt'}
        </Button>
      </div>

      {(showCreateForm || editingPrompt) && (
        <Card>
          <CardHeader>
            <CardTitle>{editingPrompt ? 'Edit Prompt' : 'Create New Prompt'}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium">Name</label>
              <input
                type="text"
                className="w-full mt-1 p-2 border rounded-md"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="Enter prompt name"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Stage</label>
              <select
                className="w-full mt-1 p-2 border rounded-md"
                value={formData.stage}
                onChange={(e) => setFormData({ ...formData, stage: e.target.value })}
              >
                <option value="story">Story</option>
                <option value="character">Character</option>
                <option value="scene">Scene</option>
                <option value="manifest">Manifest</option>
              </select>
            </div>
            <div>
              <label className="text-sm font-medium">Genre</label>
              <input
                type="text"
                className="w-full mt-1 p-2 border rounded-md"
                value={formData.genre}
                onChange={(e) => setFormData({ ...formData, genre: e.target.value })}
                placeholder="Enter genre"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Style</label>
              <input
                type="text"
                className="w-full mt-1 p-2 border rounded-md"
                value={formData.style}
                onChange={(e) => setFormData({ ...formData, style: e.target.value })}
                placeholder="Enter style"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Content</label>
              <textarea
                className="w-full mt-1 p-2 border rounded-md"
                value={formData.content}
                onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                placeholder="Enter prompt content"
                rows={5}
              />
            </div>
            <Button onClick={handleSubmit} disabled={createMutation.isPending || updateMutation.isPending}>
              {createMutation.isPending || updateMutation.isPending ? 'Saving...' : (editingPrompt ? 'Update' : 'Create')}
            </Button>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {prompts.length === 0 ? (
          <Card>
            <CardContent className="pt-6">
              <p className="text-muted-foreground">No prompts yet</p>
            </CardContent>
          </Card>
        ) : (
          prompts.map((prompt) => (
            <Card key={prompt.template_id || prompt.id}>
              <CardHeader>
                <CardTitle className="text-lg">{prompt.name}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-2">
                  Stage: {prompt.stage || prompt.type}
                </p>
                <p className="text-sm text-muted-foreground mb-4 line-clamp-3">
                  {prompt.content || 'No content'}
                </p>
                <div className="flex space-x-2">
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={() => handleEdit(prompt)}
                  >
                    Edit
                  </Button>
                  <Button 
                    variant="destructive" 
                    size="sm"
                    onClick={() => {
                      if (confirm('Are you sure you want to delete this prompt?')) {
                        deleteMutation.mutate((prompt.template_id || prompt.id) as string);
                      }
                    }}
                  >
                    Delete
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
