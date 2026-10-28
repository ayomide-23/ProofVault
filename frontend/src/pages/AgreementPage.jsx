import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api";
import { useauth } from "../auth";

const EXPLORER = "https://testnet.monadscan.com/tx/";

function Shell({ children }) {
  return (
    <div className="page">
      <div className="card w-full max-w-lg flex flex-col gap-5">{children}</div>
    </div>
  );
}

export default function AgreementPage() {
  const { id } = useParams();
  const { user } = useauth();
  const [agreement, setAgreement] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [agreed, setAgreed] = useState(false);
  const [signing, setSigning] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        setAgreement(await api.get_agreement(id));
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id]);

  async function handleSign() {
    setError("");
    setSigning(true);
    try {
      setAgreement(await api.sign(id, user.id));
    } catch (e) {
      setError(e.message);
    } finally {
      setSigning(false);
    }
  }

  function copyLink() {
    navigator.clipboard.writeText(window.location.href);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }

  if (loading)
    return (
      <Shell>
        <p>Loading...</p>
      </Shell>
    );
  if (!agreement) {
    return (
      <Shell>
        <h1 className="text-3xl">Not found</h1>
        <p className="error">{error || "This agreement doesn't exist."}</p>
        <Link to="/home" className="underline">
          Back to my deals
        </Link>
      </Shell>
    );
  }

  const isCounterparty = agreement.counterparty_id === user.id;
  const isCreator = agreement.creator_id === user.id;

  const details = (
    <>
      <h1 className="text-3xl underline decoration-wavy decoration-gold decoration-4 underline-offset-8">
        {agreement.title}
      </h1>
      <p className="whitespace-pre-wrap">{agreement.terms}</p>
      {agreement.price != null && (
        <p className="font-display text-2xl">
          ₦{agreement.price.toLocaleString()}
        </p>
      )}
    </>
  );

  // Locked: proof view
  if (agreement.counterparty_signed) {
    const tx = agreement.tx_hash?.startsWith("0x")
      ? agreement.tx_hash
      : `0x${agreement.tx_hash}`;
    return (
      <Shell>
        <div className="stamp animate-slam self-end [--slam-delay:0s]">
          SIGNED ✓
        </div>
        {details}
        <div className="border-t-[3px] border-dashed border-ink pt-4 text-base break-all flex flex-col gap-2">
          <p>
            <b>Locked on:</b>{" "}
            {new Date(agreement.confirmed_at).toLocaleString()}
          </p>
          <details className="text-base">
            <summary className="cursor-pointer font-display">
              Technical details
            </summary>
            <p className="mt-2 break-all">
              <b>Fingerprint:</b> {agreement.fingerprint_hash}
            </p>
          </details>
          <a
            href={`${EXPLORER}${tx}`}
            target="_blank"
            rel="noreferrer"
            className="underline font-display"
          >
            View proof on Monad ↗
          </a>
        </div>
        <Link to="/home" className="text-center underline">
          Back to my deals
        </Link>
      </Shell>
    );
  }

  // Pending: the other person reviews and signs
  if (isCounterparty) {
    return (
      <Shell>
        {details}
        <label className="flex gap-3 items-start cursor-pointer">
          <input
            type="checkbox"
            className="mt-1 w-5 h-5 accent-black"
            checked={agreed}
            onChange={(e) => setAgreed(e.target.checked)}
          />
          <span>I have read these terms and I agree to them.</span>
        </label>
        {error && <span className="error">{error}</span>}
        <button
          className="btn w-full"
          disabled={!agreed || signing}
          onClick={handleSign}
        >
          {signing ? "Locking it in..." : "Sign this agreement"}
        </button>
        <Link to="/home" className="text-center underline">
          Not now
        </Link>
      </Shell>
    );
  }

  // Pending: creator is waiting
  if (isCreator) {
    return (
      <Shell>
        {details}
        <p className="font-display text-xl">Waiting for them to sign.</p>
        <button className="btn" onClick={copyLink}>
          {copied ? "Copied!" : "Copy link"}
        </button>
        <Link to="/home" className="text-center underline">
          Back to my deals
        </Link>
      </Shell>
    );
  }

  // Pending: neither party
  return (
    <Shell>
      <h1 className="text-3xl">This one isn't for you</h1>
      <p>This agreement is between two other people.</p>
      <Link to="/home" className="underline">
        Back to my deals
      </Link>
    </Shell>
  );
}
