import { useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import { useauth } from "../auth";

export default function CreateAgreement() {
  const { user } = useauth();
  const [form, setForm] = useState({ title: "", terms: "", price: "", counterparty_phone: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [created, setCreated] = useState(null);
  const [copied, setCopied] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  async function handleSubmit(e) {
    e.preventDefault();
    if (!/^\+234[789]\d{9}$/.test(form.counterparty_phone)) {
      setError("Enter their number as +234XXXXXXXXXX");
      return;
    }
    if (form.counterparty_phone === user.phone_number) {
      setError("You can't make an agreement with yourself");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const agreement = await api.create_agreement({
        title: form.title,
        terms: form.terms,
        creator_id: user.id,
        counterparty_phone: form.counterparty_phone,
        price: form.price ? Number(form.price) : null,
      });
      setCreated(agreement);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function copyLink(link) {
    navigator.clipboard.writeText(link);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }

  if (created) {
    const link = `${window.location.origin}/agreements/${created.id}`;
    return (
      <div className="page">
        <div className="card w-full max-w-md flex flex-col gap-5">
          <h1 className="text-3xl underline decoration-wavy decoration-gold decoration-4 underline-offset-8">Deal written ✍️</h1>
          <p>Send this link to {form.counterparty_phone}. They sign, and it gets locked.</p>
          <input className="input" readOnly value={link} />
          <button className="btn" onClick={() => copyLink(link)}>{copied ? "Copied!" : "Copy link"}</button>
          <Link to="/home" className="text-center underline">Back to my deals</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <form className="card w-full max-w-md flex flex-col gap-5" onSubmit={handleSubmit}>
        <h1 className="text-3xl underline decoration-wavy decoration-gold decoration-4 underline-offset-8">New agreement</h1>
        <input className="input" name="title" placeholder="Title (e.g. AC repair)" value={form.title} onChange={handleChange} required />
        <textarea className="input" name="terms" placeholder="What exactly was agreed?" value={form.terms} onChange={handleChange} required />
        <input className="input" name="price" type="number" min="0" placeholder="Price in ₦ (optional)" value={form.price} onChange={handleChange} />
        <input className="input" name="counterparty_phone" placeholder="Their number (+234...)" value={form.counterparty_phone} onChange={handleChange} required />
        {error && <span className="error">{error}</span>}
        <button className="btn w-full" disabled={loading}>{loading ? "Please wait..." : "Create agreement"}</button>
        <Link to="/home" className="text-center underline">Cancel</Link>
      </form>
    </div>
  );
}