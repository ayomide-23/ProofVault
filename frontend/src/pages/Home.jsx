import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import { useauth } from "../auth";
import AgreementCard from "../components/AgreementCard";

function Section({ title, items, mode }) {
  if (items.length === 0) return null;
  return (
    <section className="mt-10">
      <h2 className="text-2xl mb-4 underline decoration-wavy decoration-gold decoration-4 underline-offset-8">{title}</h2>
      <div className="grid gap-5 sm:grid-cols-2">
        {items.map((a, i) => <AgreementCard key={a.id} agreement={a} mode={mode} index={i} />)}
      </div>
    </section>
  );
}

export default function Home() {
  const { user, logout } = useauth();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
        try{
            const data = await api.list_agreements(user.id);
            setItems(data);
        }catch(err){
            setError(err.message)
        }finally{
            setLoading(false)
        }
    }
    load()
  }, [user.id])

  const locked  = items.filter((a) => a.counterparty_signed);
  const turn    = items.filter((a) => !a.counterparty_signed && a.counterparty_id === user.id);
  const waiting = items.filter((a) => !a.counterparty_signed && a.creator_id === user.id);

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <header className="flex items-center justify-between gap-4">
        <h1 className="text-3xl sm:text-4xl">Hey {user.name || user.phone_number} 👋</h1>
        <button onClick={logout} className="underline">Log out</button>
      </header>

      {locked.length > 0 && <p className="mt-1 opacity-70">{locked.length} deal{locked.length > 1 ? "s" : ""} locked</p>}

      <Link to="/new" className="btn inline-block text-center text-2xl py-4 w-full sm:w-auto mt-6">
        + New agreement
      </Link>

      {loading && <p className="mt-10">Loading your deals...</p>}
      {error && <p className="error mt-10">{error}</p>}

      {!loading && !error && items.length === 0 && (
        <div className="card mt-10 text-center">
          <p className="text-2xl font-display">No deals yet.</p>
          <p>Write your first one and lock it in. ✍️</p>
        </div>
      )}

      <Section title="Waiting for your signature" items={turn} mode="turn" />
      <Section title="Waiting for them" items={waiting} mode="waiting" />
      <Section title="Locked ✓" items={locked} mode="locked" />
    </div>
  );
}