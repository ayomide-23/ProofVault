import { useState } from "react";
import { useNavigate } from "react-router-dom";

const STICKERS = {
  turn:    { text: "YOUR TURN", cls: "bg-gold" },
  waiting: { text: "PENDING",   cls: "bg-white" },
  locked:  { text: "LOCKED ✓",  cls: "bg-mint" },
};

export default function AgreementCard({ agreement, mode, index }) {
  const navigate = useNavigate();
  const [copied, setCopied] = useState(false);
  const sticker = STICKERS[mode];

  function copyLink(e) {
    e.stopPropagation();
    navigator.clipboard.writeText(`${window.location.origin}/agreements/${agreement.id}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }

  return (
    <div
      onClick={() => navigate(`/agreements/${agreement.id}`)}
      className={`note ${mode === "turn" ? "bg-gold" : ""} ${index % 2 ? "rotate-1" : "-rotate-1"}`}
    >
      <span className={`sticker ${sticker.cls}`}>{sticker.text}</span>
      <h3 className="text-2xl mt-2">{agreement.title}</h3>
      <p className="opacity-70">with {agreement.other_party_name || agreement.other_party_phone}</p>
      {agreement.price != null && <p className="font-display text-xl mt-1">₦{agreement.price.toLocaleString()}</p>}
      {mode === "waiting" && (
        <button className="btn text-base! py-1! mt-3" onClick={copyLink}>
          {copied ? "Copied!" : "Copy link"}
        </button>
      )}
    </div>
  );
}