import { QueryProvider } from '@/providers/query_provider';
import { WebSocketProvider } from '@/providers/websocket_provider';
import { ThemeProvider } from '@/providers/theme_provider';
import { AuthProvider } from '@/providers/auth_provider';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider>
          <AuthProvider>
            <QueryProvider>
              <WebSocketProvider>{children}</WebSocketProvider>
            </QueryProvider>
          </AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
