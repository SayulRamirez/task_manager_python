import { inject, Injectable } from "@angular/core";
import { ApiService } from "./api.service";
import { HttpHeaders, HttpParams } from "@angular/common/http";

export interface UserRegister {
    email: string;
    firstName: string;
    lastName: string;
    maternalSurname: string | undefined;
    phoneNumber: string;
    password: string;
}

export interface UserResponse {
    email: string;
    firtName: string;
    lastName: string;
    maternalSurname: string | undefined;
    phoneNumber: string;
    id: number;
}

export interface LoginRequest {
    username: string;
    password: string
}

@Injectable({ providedIn: "root" })
export class AuthService {
    private apiService = inject(ApiService);
    
    private authLogin = 'auth/login';
    private authLogout = 'auth/logout';
    private authRegister = 'auth/register';

    login(credentials: LoginRequest) {
        const body = new HttpParams()
            .set('username', credentials.username)
            .set('password', credentials.password);

        const headers = new HttpHeaders({
            'Content-Type': 'application/x-www-form-urlencoded'
        });

        return this.apiService.post(this.authLogin, body.toString(), headers);
    }

    logout() {
        return this.apiService.post(this.authLogout);
    }

    register(user: UserRegister) {
        return this.apiService.post<UserResponse>(this.authRegister, user);
    }

}