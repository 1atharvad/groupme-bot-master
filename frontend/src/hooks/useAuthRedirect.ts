'use client';

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export const useAuthRedirect = () => {
  const router = useRouter();

  useEffect(() => {
    if (["/admin", "/admin/"].includes(window.location.pathname)) {
      const urlParams = new URLSearchParams(window.location.search);
      const accessToken = urlParams.get("access_token");
      const storedToken = sessionStorage.getItem("access_token");

      if (!storedToken) {
        if (!accessToken) {
          router.push("/login");
        } else {
          sessionStorage.setItem("access_token", accessToken);
          window.history.replaceState({}, document.title, window.location.pathname);
        }
      } else {
        window.history.replaceState({}, document.title, window.location.pathname);
      }
    }
  }, [router]);
};
