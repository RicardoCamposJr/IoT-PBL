export default function Modal() {
  return (
    <div>
      <h3>Insira a nova temperatura:</h3>
      <input type="number" name="tempChange" id="tempChange" />
      <div>
        <a href="" onClick={closeModal}>Mudar</a>
      </div>
    </div>
  )
}