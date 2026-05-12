'use client';

import Link from 'next/link';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { ConnectionStatus } from '@/components/realtime/connection_status';
import { GenerateVideoPanel } from '@/components/generate/generate_video_panel';
import { Video, Briefcase, List, Settings, Sparkles, Zap, Layers, BarChart3, ArrowRight } from 'lucide-react';

export default function DashboardPage() {
  return (
    <div className="relative min-h-screen">
      {/* Animated gradient background */}
      <div className="gradient-bg" />
      
      {/* Main content */}
      <div className="relative z-10 py-8">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="mb-12">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
              <div>
                <h1 className="text-5xl font-bold gradient-text mb-3">
                  AI Video Platform
                </h1>
                <p className="text-xl text-muted-foreground max-w-2xl">
                  Создавайте потрясающие видео из текстовых описаний с помощью передовых AI моделей
                </p>
              </div>
              <div className="flex items-center gap-3">
                <ConnectionStatus />
              </div>
            </div>
            
            {/* Main Call to Action - Glass Card */}
            <Card className="glass-card overflow-hidden border-0 hover-lift">
              <div className="absolute top-0 right-0 w-64 h-64 bg-primary/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
              <div className="absolute bottom-0 left-0 w-64 h-64 bg-secondary/10 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2" />
              
              <CardHeader className="relative pb-4">
                <div className="flex items-center gap-3 mb-2">
                  <div className="p-2 rounded-lg bg-primary/10 glow-primary">
                    <Sparkles className="h-6 w-6 text-primary" />
                  </div>
                  <CardTitle className="text-3xl font-bold">
                    Создайте своё первое видео
                  </CardTitle>
                </div>
                <p className="text-muted-foreground text-lg">
                  Просто опишите идею вашего видео, и наш AI позаботится обо всём — от генерации сценария до финального рендера
                </p>
              </CardHeader>
              
              <CardContent className="relative">
                <div className="w-full"><GenerateVideoPanel /></div>
              </CardContent>
            </Card>
          </div>

          {/* Stats Bar */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            {[
              { label: 'Проектов', value: '12', icon: Video, color: 'text-blue-500' },
              { label: 'Задач', value: '8', icon: Briefcase, color: 'text-green-500' },
              { label: 'Промптов', value: '24', icon: List, color: 'text-purple-500' },
              { label: 'Рендеров', value: '5', icon: Zap, color: 'text-yellow-500' },
            ].map((stat, i) => (
              <Card key={i} className="glass-card hover-lift border-0">
                <CardContent className="p-4 flex items-center gap-3">
                  <stat.icon className={`h-8 w-8 ${stat.color}`} />
                  <div>
                    <p className="text-2xl font-bold">{stat.value}</p>
                    <p className="text-sm text-muted-foreground">{stat.label}</p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Features Grid */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {/* Projects */}
            <Card className="glass-card hover-lift border-0 group cursor-pointer">
              <CardHeader className="pb-4">
                <div className="flex items-center justify-between mb-4">
                  <div className="p-3 rounded-xl bg-gradient-to-br from-blue-500 to-blue-600 glow-secondary shadow-lg">
                    <Video className="h-6 w-6 text-white" />
                  </div>
                  <ArrowRight className="h-5 w-5 text-muted-foreground group-hover:translate-x-1 transition-transform" />
                </div>
                <CardTitle className="text-xl font-semibold">
                  Проекты
                </CardTitle>
                <p className="text-muted-foreground mt-2">
                  Управляйте и организуйте свои видеопроекты в одном месте
                </p>
              </CardHeader>
              <CardContent>
                <Link href="/projects" className="inline-flex items-center text-sm font-medium text-primary hover:text-primary/80 transition-colors">
                  Открыть проекты
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </CardContent>
            </Card>

            {/* Jobs */}
            <Card className="glass-card hover-lift border-0 group cursor-pointer">
              <CardHeader className="pb-4">
                <div className="flex items-center justify-between mb-4">
                  <div className="p-3 rounded-xl bg-gradient-to-br from-green-500 to-green-600 glow-success shadow-lg">
                    <Briefcase className="h-6 w-6 text-white" />
                  </div>
                  <ArrowRight className="h-5 w-5 text-muted-foreground group-hover:translate-x-1 transition-transform" />
                </div>
                <CardTitle className="text-xl font-semibold">
                  Задачи
                </CardTitle>
                <p className="text-muted-foreground mt-2">
                  Отслеживайте и управляйте задачами рендеринга в реальном времени
                </p>
              </CardHeader>
              <CardContent>
                <Link href="/jobs" className="inline-flex items-center text-sm font-medium text-primary hover:text-primary/80 transition-colors">
                  Просмотр задач
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </CardContent>
            </Card>

            {/* Prompts */}
            <Card className="glass-card hover-lift border-0 group cursor-pointer">
              <CardHeader className="pb-4">
                <div className="flex items-center justify-between mb-4">
                  <div className="p-3 rounded-xl bg-gradient-to-br from-purple-500 to-purple-600 glow-accent shadow-lg">
                    <List className="h-6 w-6 text-white" />
                  </div>
                  <ArrowRight className="h-5 w-5 text-muted-foreground group-hover:translate-x-1 transition-transform" />
                </div>
                <CardTitle className="text-xl font-semibold">
                  Промпты
                </CardTitle>
                <p className="text-muted-foreground mt-2">
                  Создавайте и переиспользуйте AI промпты для стабильных результатов
                </p>
              </CardHeader>
              <CardContent>
                <Link href="/prompts" className="inline-flex items-center text-sm font-medium text-primary hover:text-primary/80 transition-colors">
                  Управление промптами
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </CardContent>
            </Card>

            {/* Render */}
            <Card className="glass-card hover-lift border-0 group cursor-pointer">
              <CardHeader className="pb-4">
                <div className="flex items-center justify-between mb-4">
                  <div className="p-3 rounded-xl bg-gradient-to-br from-indigo-500 to-indigo-600 glow-secondary shadow-lg">
                    <Layers className="h-6 w-6 text-white" />
                  </div>
                  <ArrowRight className="h-5 w-5 text-muted-foreground group-hover:translate-x-1 transition-transform" />
                </div>
                <CardTitle className="text-xl font-semibold">
                  Рендер
                </CardTitle>
                <p className="text-muted-foreground mt-2">
                  Мониторьте прогресс рендеринга и готовые результаты
                </p>
              </CardHeader>
              <CardContent>
                <Link href="/render" className="inline-flex items-center text-sm font-medium text-primary hover:text-primary/80 transition-colors">
                  Очередь рендера
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </CardContent>
            </Card>

            {/* Analytics */}
            <Card className="glass-card hover-lift border-0 group cursor-pointer">
              <CardHeader className="pb-4">
                <div className="flex items-center justify-between mb-4">
                  <div className="p-3 rounded-xl bg-gradient-to-br from-yellow-500 to-orange-500 glow-warning shadow-lg">
                    <BarChart3 className="h-6 w-6 text-white" />
                  </div>
                  <ArrowRight className="h-5 w-5 text-muted-foreground group-hover:translate-x-1 transition-transform" />
                </div>
                <CardTitle className="text-xl font-semibold">
                  Аналитика
                </CardTitle>
                <p className="text-muted-foreground mt-2">
                  Отслеживайте метрики производительности и использования
                </p>
              </CardHeader>
              <CardContent>
                <Link href="/analytics" className="inline-flex items-center text-sm font-medium text-primary hover:text-primary/80 transition-colors">
                  Смотреть аналитику
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </CardContent>
            </Card>

            {/* Settings */}
            <Card className="glass-card hover-lift border-0 group cursor-pointer">
              <CardHeader className="pb-4">
                <div className="flex items-center justify-between mb-4">
                  <div className="p-3 rounded-xl bg-gradient-to-br from-gray-600 to-gray-700 shadow-lg">
                    <Settings className="h-6 w-6 text-white" />
                  </div>
                  <ArrowRight className="h-5 w-5 text-muted-foreground group-hover:translate-x-1 transition-transform" />
                </div>
                <CardTitle className="text-xl font-semibold">
                  Настройки
                </CardTitle>
                <p className="text-muted-foreground mt-2">
                  Настройте AI модели и персональные предпочтения
                </p>
              </CardHeader>
              <CardContent>
                <Link href="/settings" className="inline-flex items-center text-sm font-medium text-primary hover:text-primary/80 transition-colors">
                  Конфигурация
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
