"use client"

import { useRouter } from "next/navigation"
import { LanguageProvider } from "@/hooks/use-language"
import { useWallet } from "@/hooks/use-wallet"
import { UserDashboard } from "@/components/user-dashboard"
import { LiveTicker } from "@/components/live-ticker"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Wallet, Loader2, Key, CreditCard } from "lucide-react"
import Image from "next/image"
import Link from "next/link"
import { BANXA_CHECKOUT_URL } from "@/lib/constants"

function DashboardContent() {
  const router = useRouter()
  const { isConnected, connect, isConnecting, hasMetaMask, error } = useWallet()

  if (isConnected) {
    return (
      <>
        <LiveTicker />
        <UserDashboard />
      </>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <LiveTicker />
      <div className="flex items-center justify-center p-4 min-h-[calc(100vh-36px)]">
        <Card className="w-full max-w-md border-[#D4A537]/20 terminal-card">
          <CardContent className="flex flex-col items-center text-center p-8 space-y-6">
            <div className="relative w-24 h-24 animate-pulse-glow rounded-full overflow-hidden border-2 border-[#D4A537]/30">
              <Image src="/images/opm-logo-200.png" alt="OnePremium" fill className="object-cover" />
            </div>

            <div className="space-y-2">
              <h1 className="text-2xl font-serif font-bold text-foreground">
                Connect to <span className="text-[#D4A537]">Dashboard</span>
              </h1>
              <p className="text-muted-foreground text-sm">Choose your preferred wallet connection method</p>
            </div>

            {error && (
              <div className="w-full p-3 rounded-lg bg-destructive/10 border border-destructive/20 text-sm text-destructive">
                {error}
              </div>
            )}

            <div className="w-full space-y-3">
              {hasMetaMask && (
                <Button
                  onClick={connect}
                  disabled={isConnecting}
                  className="w-full h-12 gap-2 bg-[#D4A537] hover:bg-[#B8912E] text-black font-semibold"
                >
                  {isConnecting ? (
                    <><Loader2 className="h-5 w-5 animate-spin" /> Connecting...</>
                  ) : (
                    <><Wallet className="h-5 w-5" /> Connect MetaMask</>
                  )}
                </Button>
              )}

              <Link href="/wallet" className="block">
                <Button variant="outline" className="w-full h-12 gap-2 border-[#D4A537]/30 text-foreground">
                  <Key className="h-5 w-5" /> OPM Wallet (Non-Custodial)
                </Button>
              </Link>

              <a href={BANXA_CHECKOUT_URL} target="_blank" rel="noopener noreferrer" className="block">
                <Button variant="outline" className="w-full h-12 gap-2 border-[#D4A537]/30 text-foreground">
                  <CreditCard className="h-5 w-5" /> Buy Crypto with EUR
                </Button>
              </a>
            </div>

            <Button variant="ghost" onClick={() => router.push("/")} className="text-muted-foreground text-sm">
              Back to Home
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default function DashboardPage() {
  return (
    <LanguageProvider>
      <DashboardContent />
    </LanguageProvider>
  )
}
