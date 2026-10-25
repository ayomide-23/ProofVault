import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useauth } from "../auth";
import { api } from "../api";
import Doodles from "../components/Doodles";

export default function Login() {
  const [user, setuser] = useState({
    phone_number: "",
    name: "",
  });
  const [error, seterror] = useState({});
  const [isloading, setisloading] = useState(false);
  const { login } = useauth();
  const navigate = useNavigate();
  const [params] = useSearchParams();

  const handlechange = (e) => {
    const { name, value } = e.target;
    setuser((prev) => ({ ...prev, [name]: value }));
  };

  const validate = () => {
    const new_error = {};
    if (user.phone_number.length < 11) {
      new_error.phone_number = "Phone number must be at least 11 digits";
    }
    return new_error;
  };

  async function handlesubmit(e) {
    e.preventDefault();
    const validate_errors = validate();
    if (Object.keys(validate_errors).length > 0) {
      seterror(validate_errors);
      return;
    }
    seterror({});
    setisloading(true);
    try {
      const loggedin_user = await api.login(
        user.phone_number,
        user.name || null,
      );
      login(loggedin_user);
      navigate(params.get("next") || "/");
    } catch (err) {
      seterror({ detail: err.message });
    } finally {
      setisloading(false);
    }
  }

  return (
    <div className="page relative">
      <Doodles />
      <div className="relative z-10 w-full max-w-md">
        <form onSubmit={handlesubmit} className="card flex flex-col gap-5">
          <h1 className="text-3xl sm:text-3xl underline decoration-wavy decoration-4 underline-offset-8">
            ProofVault
          </h1>
          <input
            className="input"
            placeholder="Phone number (+234...)"
            name="phone_number"
            value={user.phone_number}
            onChange={handlechange}
            required
          />
          <input
            className="input"
            placeholder="Name"
            name="name"
            value={user.name}
            onChange={handlechange}
          />
          {error.phone_number && <span className="error">{error.phone}</span>}
          {error.detail && <span className="error">{error.detail}</span>}

          <button
            disabled={isloading}
            className="btn w-full sm:w-auto sm:self-start"
          >
            {isloading ? "Please wait..." : "Continue"}
          </button>
        </form>
      </div>
    </div>
  );
}
