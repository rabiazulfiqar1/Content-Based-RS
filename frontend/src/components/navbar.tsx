"use client"

import type React from "react"

import Link from "next/link"
import { usePathname, useRouter } from "next/navigation"
import { cn } from "@/lib/utils"
import { Search, User } from "lucide-react"
import { supabase } from "@/lib/supabaseClient"
import { useEffect, useState } from "react"
import type { User as SupabaseUser } from "@supabase/supabase-js"
import { ProfileDialogContent } from "@/components/profile-dialog-content"

export function Navbar() {
  const pathname = usePathname()
  const router = useRouter()
  const [user, setUser] = useState<SupabaseUser | null>(null)
  const [isProfileDialogOpen, setIsProfileDialogOpen] = useState(false)
  const [userName, setUserName] = useState<string>("")
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const initializeAuth = async () => {
      const { data: { session } } = await supabase.auth.getSession()
      setUser(session?.user ?? null)

      if (session?.user) {
        try {
          const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api"
          const response = await fetch(`${API_BASE_URL}/users/${session.user.id}/basic-profile`)
          if (response.ok) {
            const data = await response.json()
            setUserName(data.full_name || session.user.email || "User")
          } else {
            setUserName(session.user.email || "User")
          }
        } catch (error) {
          setUserName(session.user.email || "User")
        }
      }
      setIsLoading(false)
    }

    initializeAuth()

    // Listen for auth changes (login/logout only)
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange(async (_event, session) => {
      setUser(session?.user ?? null)
      
      if (session?.user) {
        try {
          const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api"
          const response = await fetch(`${API_BASE_URL}/users/${session.user.id}/basic-profile`)
          if (response.ok) {
            const data = await response.json()
            setUserName(data.full_name || session.user.email || "User")
          } else {
            setUserName(session.user.email || "User")
          }
        } catch (error) {
          setUserName(session.user.email || "User")
        }
      } else {
        setUserName("")
      }
    })

    return () => subscription.unsubscribe()
  }, []) // Empty dependency array = runs once on mount

  const handleNavigation = (e: React.MouseEvent<HTMLAnchorElement>, href: string) => {
    if (!user && href !== "/") {
      e.preventDefault()
      router.push("/signup")
    }
  }

  const navItems = [
    { href: "/", label: "Home" },
    { href: "/projects/search", label: "Search Projects", icon: Search },
  ]

  return (
    <>
      <nav className="border-b border-white/10 bg-white/5 backdrop-blur-md">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            {/* Logo */}
            <Link href="/" className="flex items-center gap-2 font-semibold text-lg text-white">
              <div className="h-8 w-8 rounded-lg bg-cyan-600 flex items-center justify-center text-white">◆</div>
              <span className="hidden sm:inline">ProjectMatch</span>
            </Link>

            {/* Nav Items */}
            <div className="flex items-center gap-1">
              {navItems.map(({ href, label, icon: Icon }) => (
                <Link
                  key={href}
                  href={href}
                  onClick={(e) => handleNavigation(e, href)}
                  className={cn(
                    "flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                    pathname === href
                      ? "bg-cyan-600 text-white"
                      : "text-white/70 hover:bg-white/10 hover:text-cyan-400",
                  )}
                >
                  {Icon && <Icon className="h-4 w-4" />}
                  <span className="hidden sm:inline">{label}</span>
                </Link>
              ))}

              {!isLoading && (
                user ? (
                  <>
                    <Link
                      href="/profile"
                      className={cn(
                        "flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                        pathname === "/profile" || pathname.startsWith("/profile/")
                          ? "bg-cyan-600 text-white"
                          : "text-white/70 hover:bg-white/10 hover:text-cyan-400",
                      )}
                      aria-label="Go to profile page"
                    >
                      <User className="h-4 w-4" />
                      <span className="hidden sm:inline">Profile</span>
                    </Link>
                    <button
                      onClick={() => setIsProfileDialogOpen(true)}
                      className="ml-2 h-10 w-10 rounded-full bg-gradient-to-br from-cyan-400 to-cyan-600 flex items-center justify-center text-white font-semibold hover:from-cyan-500 hover:to-cyan-700 transition-all hover:scale-105 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:ring-offset-2 focus:ring-offset-transparent"
                      aria-label="Open profile dialog"
                    >
                      {userName.charAt(0).toUpperCase()}
                    </button>
                  </>
                ) : (
                  <Link
                    href="/signup"
                    className="flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium bg-cyan-600 text-white hover:bg-cyan-700 transition-colors"
                  >
                    Sign In
                  </Link>
                )
              )}
            </div>
          </div>
        </div>
      </nav>

      <ProfileDialogContent open={isProfileDialogOpen} onOpenChange={setIsProfileDialogOpen} user={user} />
    </>
  )
}