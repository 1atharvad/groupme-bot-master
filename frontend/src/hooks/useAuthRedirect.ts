import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const useAuthRedirect = () => {
  const navigate = useNavigate();

  useEffect(() => {
    if (["/admin", "/admin/"].includes(window.location.pathname)) {
      const urlParams = new URLSearchParams(window.location.search);
      const accessToken = urlParams.get("access_token");
      const storedToken = sessionStorage.getItem("access_token");

      if (!storedToken) {
        if (!accessToken) {
          navigate("/login/");
        } else {
          sessionStorage.setItem("access_token", accessToken);
          window.history.replaceState({}, document.title, window.location.pathname);
        }
      } else {
        window.history.replaceState({}, document.title, window.location.pathname);
      }
    }
  }, [navigate]);
};

export default useAuthRedirect;
