'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { promptsApi } from '@/modules/prompts/api/prompts_api';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import type { PromptTemplate } from '@/modules/prompts/types/prompts_types';
import type { PromptCategory } from '@/modules/prompts/types/prompts_types';

export default function PromptsPage() {
  const queryClient = useQueryClient();
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingPrompt, setEditingPrompt] = useState<PromptTemplate | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    category: 'story' as PromptCategory,
    content: '',
    genre_tags: [] as string[],
    channel_tags: [] as string[],
  });

  const { data: prompts = [], isLoading, error } = useQuery({
    queryKey: ['prompts-module'],
    queryFn: () => promptsApi.getAll(),
  });

  const createMutation = useMutation({
    mutationFn: (data: Partial<PromptTemplate>) => {
      const payload = {
        ...data,
        variables: [],
        is_active: true,
      };
      return promptsApi.create(payload as any);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['prompts-module'] });
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
      queryClient.invalidateQueries({ queryKey: ['prompts-module'] });
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
      queryClient.invalidateQueries({ queryKey: ['prompts-module'] });
      alert('Prompt deleted successfully!');
    },
    onError: (error) => {
      alert(`Failed to delete prompt: ${error.message}`);
    },
  });

  const resetForm = () => {
    setFormData({
      name: '',
      category: 'story',
      content: '',
      genre_tags: [],
      channel_tags: [],
    });
  };

  const handleEdit = (prompt: PromptTemplate) => {
    setEditingPrompt(prompt);
    setFormData({
      name: prompt.name || '',
      category: prompt.category || 'story',
      content: prompt.content || '',
      genre_tags: prompt.genre_tags || [],
      channel_tags: prompt.channel_tags || [],
    });
    setShowCreateForm(false);
  };

  const handleSubmit = () => {
    if (editingPrompt) {
      updateMutation.mutate({ id: editingPrompt.id, data: formData });
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
              <label className="text-sm font-medium">Category</label>
              <select
                className="w-full mt-1 p-2 border rounded-md"
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value as PromptCategory })}
              >
                <option value="story">Story</option>
                <option value="characters">Characters</option>
                <option value="scenes">Scenes</option>
                <option value="tts">TTS</option>
                <option value="subtitles">Subtitles</option>
                <option value="metadata">Metadata</option>
                <option value="render">Render</option>
              </select>
            </div>
            <div>
              <label className="text-sm font-medium">Genre Tags (comma-separated)</label>
              <input
                type="text"
                className="w-full mt-1 p-2 border rounded-md"
                value={formData.genre_tags.join(', ')}
                onChange={(e) => setFormData({
                  ...formData,
                  genre_tags: e.target.value.split(',').map(s => s.trim()).filter(Boolean)
                })}
                placeholder="general, drama, comedy"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Channel Tags (comma-separated)</label>
              <input
                type="text"
                className="w-full mt-1 p-2 border rounded-md"
                value={formData.channel_tags.join(', ')}
                onChange={(e) => setFormData({
                  ...formData,
                  channel_tags: e.target.value.split(',').map(s => s.trim()).filter(Boolean)
                })}
                placeholder="youtube, tiktok, instagram"
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
            <Card key={prompt.id}>
              <CardHeader>
                <CardTitle className="text-lg">{prompt.name}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-2">
                  Category: {prompt.category}
                </p>
                <p className="text-sm text-muted-foreground mb-2">
                  Genre: {prompt.genre_tags?.join(', ') || 'general'}
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
                        deleteMutation.mutate(prompt.id);
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
