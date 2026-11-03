import { Component, input } from '@angular/core';

@Component({
  imports: [],
  selector: 'app-form-content',
  styleUrl: './form-content.css',
  templateUrl: './form-content.html',
})
export class FormContent {
  formTitle = input.required<string>();
  formMessage = input.required<string>();
  isRegister = input.required<boolean>();
}
