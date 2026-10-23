import type { Metadata } from 'next';
export const metadata:Metadata={title:'KS Digital BD',description:'Software, websites and apps for growing businesses.'};
export default function RootLayout({children}:{children:React.ReactNode}) {return <html lang="en"><body>{children}</body></html>}
