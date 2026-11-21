import './globals.css';

export const metadata = {
  title: 'LandslideNER — Early Warning & Landslide Risk Monitoring',
  description: 'AI-Based Landslide Risk & Susceptibility Monitoring System in North Eastern India (NER). BTech CSE Capstone Prototype.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-slate-50 text-slate-900 antialiased min-h-screen flex flex-col">
        {children}
      </body>
    </html>
  );
}

