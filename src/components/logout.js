import { useEffect } from "react";

const Logout = () => {
  useEffect(() => {
    localStorage.clear("token");
    window.location.replace("/login");
  });
  return null;
};

export default Logout;