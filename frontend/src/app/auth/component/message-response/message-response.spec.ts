import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MessageResponse } from './message-response';

describe('MessageResponse', () => {
  let component: MessageResponse;
  let fixture: ComponentFixture<MessageResponse>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MessageResponse],
    }).compileComponents();

    fixture = TestBed.createComponent(MessageResponse);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
