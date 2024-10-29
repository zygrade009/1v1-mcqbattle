import { Cookies } from "react-cookie";

const AuthCookies = {
  cookies: new Cookies(),

  SetAccessToken(accessToken) {
    return this.cookies.set("access_token", accessToken, {
      path: "/",
      expires: new Date(new Date().getTime() + 28 * 60 * 1000), // 28 minutes
    });
  },

  SetRefreshToken(refreshToken) {
    return this.cookies.set("refresh_token", refreshToken, {
      path: "/",
      expires: new Date(new Date().getTime() + 10000 * 60 * 1000), // Approximately 6.94 days
    });
  },

  GetAccessToken() {
    return this.cookies.get("access_token", { path: "/" });
  },

  GetRefreshToken() {
    return this.cookies.get("refresh_token", { path: "/" });
  },

  ClearAll() {
    this.cookies.remove("access_token", { path: "/" });
    this.cookies.remove("refresh_token", { path: "/" });
  }
};

export default AuthCookies;
