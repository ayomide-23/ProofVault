function Lock({ className }) {
  return (
    <svg viewBox="0 0 80 100" className={className} fill="none" stroke="#1A1A1A" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round">
      <path d="M20 45V30a20 20 0 0 1 40 0v15" />
      <rect x="10" y="45" width="60" height="48" rx="8" fill="#FFC83D" />
      <circle cx="40" cy="66" r="6" fill="#1A1A1A" />
      <path d="M40 70v10" />
    </svg>
  );
}

function Notebook({ className }) {
  return (
    <svg viewBox="0 0 160 200" className={className} fill="none" stroke="#1A1A1A" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round">
      <rect x="12" y="10" width="136" height="180" rx="10" fill="#fff" />
      {[30, 60, 90, 120].map((y) => <circle key={y} cx="12" cy={y} r="5" fill="#FFC83D" />)}
      <path d="M38 45h90M38 70h70M38 95h80" strokeWidth="3" />
      <path className="animate-draw" d="M38 140c10-20 14 10 24-6s12-16 20 0 14 8 24-4 10-4 20 2" stroke="#FF6B5E" />
    </svg>
  );
}

function Pen({ className }) {
  return (
    <svg viewBox="0 0 40 140" className={className} fill="none" stroke="#1A1A1A" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 8h16v90l-8 30-8-30z" fill="#FFC83D" />
      <path d="M12 98h16" />
    </svg>
  );
}

export default function Doodles() {
  return (
    <div aria-hidden="true" className="pointer-events-none absolute inset-0 overflow-hidden">
      <Lock className="lg:hidden absolute top-4 right-4 w-12 animate-float" />

      <div className="hidden lg:block absolute top-[12%] left-[4%] bubble animate-float -rotate-3">₦25k, done by Friday?</div>
      <div className="hidden lg:block absolute top-[24%] right-[5%] bubble bg-gold animate-float rotate-2 [animation-delay:1s]">Deal! 🤝</div>

      <Notebook className="hidden lg:block absolute bottom-[10%] left-[6%] w-44 -rotate-6 animate-float [animation-delay:.5s]" />
      <Pen className="hidden lg:block absolute bottom-[8%] left-[22%] w-8 rotate-[35deg] animate-float [animation-delay:1s]" />

      <Lock className="hidden lg:block absolute bottom-[28%] right-[14%] w-20 animate-float [animation-delay:1.5s]" />
      <div className="lg:hidden absolute bottom-6 left-4 stamp text-lg px-3 animate-slam [--slam-delay: .1s]">PROVEN ✓</div>
      <div className="hidden lg:block absolute bottom-[10%] right-[6%] stamp animate-slam">PROVEN ✓</div>
    </div>
  );
}