import { Component, inject } from '@angular/core';
import { DesktopToggle } from './component/desktop-toggle/desktop-toggle';
import { MobileToggle } from './component/mobile-toggle/mobile-toggle';
import { FormContent } from './component/form-content/form-content';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  imports: [ReactiveFormsModule, DesktopToggle, MobileToggle, FormContent],
  selector: 'app-auth',
  styleUrl: './auth.css',
  templateUrl: './auth.html',
})
export class Auth {
  isRegister = false;

  private formBuilder = inject(FormBuilder);

  formRegister = this.formBuilder.group({
    email: ['', [Validators.required, Validators.email ]],
    firstName: ['', [Validators.required, Validators.minLength(1), Validators.maxLength(20)]],
    lastName: ['', [Validators.required, Validators.minLength(1), Validators.maxLength(20)]],
    maternalSurname: ['' ,[Validators.minLength(1), Validators.maxLength(20)]],
    phoneNumber: ['', [Validators.required, Validators.minLength(10), Validators.maxLength(15)]],
    password: ['', [Validators.required, Validators.minLength(8), Validators.maxLength(64)]]
  });

  get email() { return this.formRegister.get('email')}
  get firstName() { return this.formRegister.get('firstName')}
  get lastName() { return this.formRegister.get('lastName')}
  get maternalSurname() { return this.formRegister.get('maternalSurname')}
  get phoneNumber() { return this.formRegister.get('phoneNumber')}
  get password() { return this.formRegister.get('password')}

  toggleAuth() {
    this.isRegister = !this.isRegister;
  }

  onSubmitRegister() {
    if (this.formRegister.invalid) {
      this.formRegister.markAllAsTouched();
      return;
    }

    const {
      email, 
      firstName,
      lastName,
      maternalSurname,
      phoneNumber,
      password
    } = this.formRegister.value;

    console.log('Datos listos para el backend: ', {
      email, 
      firstName,
      lastName,
      maternalSurname,
      phoneNumber,
      password
    });
  }
}