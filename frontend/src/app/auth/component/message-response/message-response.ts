import { NgClass } from '@angular/common';
import { Component, input } from '@angular/core';

@Component({
  imports: [NgClass],
  selector: 'app-message-response',
  styleUrl: './message-response.css',
  templateUrl: './message-response.html',
})
export class MessageResponse {
  message = input.required<{
    show: boolean,
    isSuccess: boolean,
    content: string
  }>();
}
