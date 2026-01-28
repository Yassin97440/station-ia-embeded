export default defineAppConfig({
  ui: {
    colors: {
      primary: 'emerald',
      neutral: 'zinc'
    },
    // Personnalisation du Header
    header: {
      slots: {
        root: 'bg-[#0a0f0d]/80 backdrop-blur-sm border-b border-emerald-900/50 sticky top-0 z-50',
        container: 'flex items-center justify-between gap-3 h-full max-w-6xl mx-auto',
        left: 'lg:flex-1 flex items-center gap-1.5',
        center: 'hidden lg:flex',
        right: 'flex items-center justify-end lg:flex-1 gap-1.5',
        title: 'shrink-0 font-bold text-xl text-white flex items-end gap-1.5'
      }
    },
    // Personnalisation du Footer
    footer: {
      slots: {
        root: 'bg-[#0a0f0d]/80 backdrop-blur-sm border-t border-emerald-900/50',
        container: 'flex flex-col md:flex-row items-center justify-between gap-4 max-w-6xl mx-auto py-6'
      }
    },
    // Personnalisation du NavigationMenu
    navigationMenu: {
      slots: {
        link: 'text-emerald-300/70 hover:text-emerald-300 transition-colors'
      }
    }
  }
})
