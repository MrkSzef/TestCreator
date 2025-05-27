interface Question {
  ID: number;
  tresc: string;
  odp: string[];
}

interface Student {
  imie: string;
  nazwisko: string;
}

interface Result {
  punkty: number;
  pytania_bledne: number[];
}

export interface ParticipantAnswer {
  klucz_odp: Record<string, string>;
  uczen: Student;
  wynik: Result;
}

interface Quiz {
  ID: string;
  zamkniety: boolean;
  pytania: Question[];
  pytania_na_arkusz: number;
  klucz_odp: Record<string, string>;
  uczestnicy_odpowiedzi: ParticipantAnswer[];
}

export interface InfoWebsocketInterface {
  quiz: Quiz;
}