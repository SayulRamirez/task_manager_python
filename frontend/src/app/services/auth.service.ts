import { inject, Injectable } from "@angular/core";
import { ApiService } from "./api.service";

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

@Injectable({ providedIn: "root" })
export class AuthService {
    private apiService = inject(ApiService);
    
    private authRegister = 'auth/register';

    register(user: UserRegister) {
        return this.apiService.post<UserResponse>(this.authRegister, user);
    }
}